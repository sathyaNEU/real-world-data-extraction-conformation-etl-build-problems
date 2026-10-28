## Tags

**Domain:** Education & Learning Sciences (item response theory and test equating).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Commission 199 new items below the Approaching cut: 27 for grade 3, 39 for grade 4, 31 for grade 5, 33 for grade 6, 49 for grade 7, 20 for grade 8.** Each workshop item's difficulty is estimated from the 2025-26 responses together with the students' abilities, with the launch items held at their 2021 values. Not the 138 that a Rasch fit of each workshop item gives with every student's ability fixed at the event's reported scale score, because those scores were computed from the writing panel's ratings and return them. Not the 93 the panel's ratings give, which put multi-step word problems that the students' answers place above the cut below it.

## 2. Critical Components

1. Items below the Approaching cut in each grade's pool once the workshop items are calibrated: grade 3 123, grade 4 111, grade 5 119, grade 6 117, grade 7 101, grade 8 130.
2. Workshop items below the cut: grade 3 60, grade 4 49, grade 5 62, grade 6 61, grade 7 46, grade 8 60.

## 3. Step-by-Step Solution

1. Took each grade's operational items from tessaline_item_bank_export_20270331.csv, the complete and incomplete events of tessaline_sessions_2025-26.csv and their scored responses in tessaline_item_responses_2025-26.parquet, dropping the unscored re-delivery rows (Corvane specification section 3): 3,894,963 responses.
2. Held each launch item at its 2021 value, theta = (QSS - 500) / 40 (scale note section 1), and estimated the 502 workshop items' difficulties by marginal maximum likelihood, the students of each window a normal population with its own mean and spread.
3. Re-estimated the launch items the same way as a check: the launch items below 452 come back within 1.0 points of their values in every grade, while read against the reported scale scores they come back 3.4 to 7.6 points too easy.
4. Counted each pool's items with difficulty below the grade's Approaching cut (scale note section 3): grade 3 123, grade 4 111, grade 5 119, grade 6 117, grade 7 101, grade 8 130.
5. Took the shortfall against Corvane's floor of 150 (specification section 5): grade 3 27, grade 4 39, grade 5 31, grade 6 33, grade 7 49, grade 8 20, 199 in all.
6. Built the import from the bank export's operational rows and qrac_item_authoring_catalog_20270315.xlsx (specification sections 1, 2 and 4): each authored item once, under the key of its latest version, so the 98 revisions Tessaline re-keyed, operational in the export under both keys, are loaded under the new key only; each item's catalog record read version by version, version 1 the full record and each later version changing only the fields its changed_fields lists, so a 2026 framework code set in the 2024 review and an enemy group set on version 1 still stand on a 2025 version that leaves them blank, and a group the 2024 review cleared (11 items) is gone; the reporting domain from the item's 2026 framework code, otherwise its 2010 standard through qrac_framework_crosswalk_2010_to_2026.csv with the crosswalk's skill-tag condition; an enemy set from each group's imported items in one grade, two or more to a set.
7. Recommendation: commission 199 new items below the Approaching cut, grade 3 27, grade 4 39, grade 5 31, grade 6 33, grade 7 49, grade 8 20.

## 4. Deliverable Answers

### bank_import_2027-28.csv

1. One row per operational item under its current key, 2,538 rows: item_key, grade, difficulty to one decimal, reporting_domain, enemy_set, interaction_type.

### pool_summary_2027-28.xlsx

1. New items to commission by grade:
   - Grade 3: 27
   - Grade 4: 39
   - Grade 5: 31
   - Grade 6: 33
   - Grade 7: 49
   - Grade 8: 20
2. Imported items by grade and 2026 framework domain:
   - Grade 3: NSO 91, ALG 129, FRA 80, MDA 50, GEO 69
   - Grade 4: NSO 96, ALG 129, FRA 68, MDA 52, GEO 64
   - Grade 5: NSO 78, ALG 128, FRA 95, MDA 61, GEO 60
   - Grade 6: PRR 101, NUM 112, ALG 73, GMS 82, DAP 59
   - Grade 7: PRR 96, NUM 90, ALG 93, GMS 78, DAP 61
   - Grade 8: PRR 9, NUM 117, ALG 169, GMS 76, DAP 72
3. Enemy sets and the items they hold, by grade:
   - Grade 3: 14 sets, 30 items
   - Grade 4: 7 sets, 16 items
   - Grade 5: 8 sets, 17 items
   - Grade 6: 11 sets, 24 items
   - Grade 7: 9 sets, 20 items
   - Grade 8: 10 sets, 23 items

### low_band_commission_memo.docx

1. The commission: 199 new items below the Approaching cut, grade 3 27, grade 4 39, grade 5 31, grade 6 33, grade 7 49, grade 8 20.
2. One chart: bars of each grade's items below the Approaching cut against the floor line at 150, each bar labelled with its count and the items to commission.
