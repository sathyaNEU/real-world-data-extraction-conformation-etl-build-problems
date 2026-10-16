# task127: the winter discharge fund's 1,200 discharge-to-assess packages across Marchshire's five acute hospitals

## Tags

**Domain:** Healthcare Delivery & Health Economics (patient flow, beds and workforce: discharge-to-assess packages).
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**Give Royal Marchford Hospital 508 packages, Wendlebury Hospital 350, Holmford Infirmary 120, Cleeve Park Hospital 222 and Ashby Vale Hospital none; they free 6,816 occupied bed-days.**

A package frees 6.39 nights a covered patient at Royal Marchford, 5.82 at Wendlebury and 5.35 at Holmford, against 4.01 at Cleeve Park and 3.14 at Ashby Vale, where most covered patients were also waiting for community equipment that a package does not bring forward. Not Ashby Vale and Cleeve Park first on their nights after the discharge ready date (10.81 and 9.86), which count those equipment waits as nights a package saves.

## 2. Critical Components

1. Covered patients last winter: Royal Marchford **508**, Wendlebury **350**, Holmford Infirmary **120**, Cleeve Park **285**, Ashby Vale **361**
2. Nights a package frees per covered patient: Royal Marchford **6.39**, Wendlebury **5.82**, Holmford Infirmary **5.35**, Cleeve Park **4.01**, Ashby Vale **3.14**

## 3. Step-by-Step Solution

1. Kept last winter's covered patients in acute_discharges_65plus_2024-12_2026-09.csv, each spell at its latest submission, per allocation note SF-2026-14 (pathway 1, a new package, a practice under NHS Marchshire ICB in gp_practices_2026-09.csv, discharge ready date 1 December 2025 to 28 February 2026): 1,624 patients.
2. Joined each to the equipment ordered for their discharge in ices_order_lines_2024-12_2026-09.csv (route Hospital discharge, which ices_export_notes.txt describes as equipment the patient needs at home from the day they go home; required by their discharge ready date; NHS number without spaces): 794 had equipment delivered, and no pathway-1 patient left before their delivery.
3. Counted for each covered patient the nights from the later of the discharge ready date and that delivery to discharge, the nights home care from the ready date would have saved (patients whose care restarted left on the later of the two), and averaged them by hospital: Royal Marchford 6.39, Wendlebury 5.82, Holmford 5.35, Cleeve Park 4.01, Ashby Vale 3.14.
4. Filled the 1,200 packages in that order, each hospital up to its covered patients, and took packages times value per the note: Royal Marchford 508, Wendlebury 350, Holmford 120, Cleeve Park 222, Ashby Vale none, 6,816 occupied bed-days.
5. Valuing a package at the nights after the ready date instead (Ashby Vale 10.81, Cleeve Park 9.86) fills Ashby Vale and Cleeve Park first and claims 10,507 bed-days, though 195 of Ashby Vale's 361 covered patients left on the day their equipment arrived.
6. Counted each night after the discharge ready date at the hospital of the patient's ward at that midnight (acute_ward_stays_2024-12_2026-09.csv, ward_reference.csv), dated to the evening it began per acute_extract_notes.txt: 24,295 occupied bed-days lost from December 2025 to February 2026.
7. Counted brokerage_referrals_2024-12_2026-09.csv by month received and care-postcode district (postcode_districts_marchshire.csv), taking the start of care bought by spot purchase from the first service_start in spot_care_invoice_lines_2025-26.csv (brokerage_ref BRK and the referral's digits): 239 of last winter's closed referrals had spot-purchased care.
8. Give Royal Marchford 508 packages, Wendlebury 350, Holmford 120, Cleeve Park 222 and Ashby Vale none, freeing 6,816 occupied bed-days.

## 4. Deliverable Answers

### d2a_package_split_winter_2026-27.xlsx

1. Packages for December 2026 to February 2027, whole packages:
   - Royal Marchford Hospital: 508
   - Wendlebury Hospital: 350
   - Holmford Infirmary: 120
   - Cleeve Park Hospital: 222
   - Ashby Vale Hospital: 0
2. Occupied bed-days each hospital's packages free, whole bed-days:
   - Royal Marchford Hospital: 3,247
   - Wendlebury Hospital: 2,037
   - Holmford Infirmary: 642
   - Cleeve Park Hospital: 890
   - Ashby Vale Hospital: 0
3. Total occupied bed-days freed: 6,816
4. Hospital that gets none: Ashby Vale Hospital
5. Referrals for home care the brokerage took with care starting no more than seven days after referral:
   - Marchford: December 2025 178, January 2026 228, February 2026 166
   - Ashby: December 2025 57, January 2026 55, February 2026 53
   - Teme Valley: December 2025 106, January 2026 103, February 2026 95

### delayed_bed_days_winter_2025-26.svg

1. Grouped bar chart, a bar for each hospital and month, each labelled with the occupied bed-days lost to delayed discharge across all pathways and, in brackets, the patients delayed:
   - Ashby Vale Hospital: December 2025 2,057 (316), January 2026 1,989 (305), February 2026 1,678 (274)
   - Royal Marchford Hospital: December 2025 2,010 (412), January 2026 1,966 (432), February 2026 1,729 (397)
   - Cleeve Park Hospital: December 2025 1,787 (293), January 2026 1,687 (277), February 2026 1,263 (220)
   - Wendlebury Hospital: December 2025 1,439 (317), January 2026 1,627 (347), February 2026 1,386 (280)
   - Holmford Infirmary: December 2025 1,109 (230), January 2026 1,381 (274), February 2026 1,187 (254)
