## Tags

**Domain:** General Statistics & Data Science (missing data, censoring and measurement error).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Accept the appraisal vendor's offer of the county-wide single-family reappraisal: the certified 2026 single-family roll fails the State Tax Commission's Rule 18-7 on both tests, a median assessment ratio of 0.87, below the rule's level band, and a coefficient of dispersion of 18, above its uniformity limit.**
Not the 2025 arm's-length sales against their 2026 values as they stand (0.95 and 8.0, inside the rule): the parcels sold in 2025 rose a median 14.9 per cent from the 2025 roll against 3.4 per cent for the rest, so those sales measure the parcels revalued after their sale, not the roll.

## 2. Critical Components

1. Single-family parcels with a 2025 arm's-length sale rose a median **14.9%** from the 2025 roll to the 2026 roll; the other single-family parcels on both rolls a median **3.4%**, most of them by their neighbourhood's common factor.
2. Those **1,742** sold parcels are **6.7%** of the **25,988** single-family parcels on the 2026 roll.
3. The study rests on **1,698** sales once the **44** whose permit work was finaled after the deed are set aside.

## 3. Step-by-Step Solution

1. Read str_rule_18-7_residential_ratio_studies.pdf: the level and the coefficient of dispersion are taken over every parcel of the class on the certified roll; market value comes from the 2025 Q deeds, each price times the index for January 2026 over the index for the deed's month (residential_price_index_tillford.csv); a sale is set aside where improvements or boundaries changed after the deed.
2. Took the Q deeds in recorder_deeds_2025.csv whose parcel number, without its dashes and with a 0 added, is an R1 parcel in assessor_roll_2026_certified.csv, and set aside the 44 whose work in building_permits_2025.csv was finaled after the deed: 1,698 sales, whose 2026 values over their indexed prices give 0.95 and 8.0.
3. Joined assessor_roll_2025_certified.xlsx to the 2026 roll on the same parcel numbers: the 1,742 parcels with a 2025 Q deed rose a median 14.9%, the parcels without one 3.4%, most of them by their neighbourhood's (nbhd_code) common change.
4. For each study sale took its 2025 value times its neighbourhood's median change among parcels without a 2025 Q deed, to the nearest 100, over its indexed price, standing for the 93.3% of the class that did not sell; its 2026 value over its indexed price stands for the 6.7% that did.
5. Weighted the two sets of 1,698 ratios by those shares (1,742 of 25,988 parcels sold): the median is 0.87 and the average absolute difference from it 18 per cent, so the class fails both tests.
6. Condominium class: the Q deeds of R2 parcels, a Wexley Commons deed signed (or permit issued) before its parcel_change_log_2025.csv entry took effect read at the new parcel identifier, a sale set aside where its unit was combined (COMBINE) or its permit work in building_permits_2025.csv finaled after the deed: 129 sales, a median of 0.93, an aggregate ratio of 0.932, a COD of 7.1 and a price-related differential of 0.997.
7. Board of Review: from board_of_review_hearings_2025.csv the hearings from 2 June 2025 on whose value_before equals the parcel's certified 2025 value (the earlier hearings are appeals of the 2024 roll), each parcel at its last hearing in its case (a case may list several parcels), REDUCED parcels summed by market area through the 2025 roll's neighbourhood and neighborhood_crosswalk.csv.
8. Recommended accepting the vendor's offer of the single-family reappraisal.

## 4. Deliverable Answers

### reappraisal_recommendation.docx

1. Accept the vendor's offer of the county-wide single-family reappraisal: the roll fails Rule 18-7.
2. Median assessment ratio of the 2026 single-family roll: 0.87
3. Coefficient of dispersion of the 2026 single-family roll: 18

### ratio_study_2026_roll.xlsx

1. Condominium class:
   - Sales the study rests on: 129
   - Median assessment ratio: 0.93
   - Aggregate assessment ratio: 0.932
   - Coefficient of dispersion: 7.1
   - Price-related differential: 0.997
2. Board of Review reductions of the 2025 roll, single-family and condominium parcels, by market area:
   - Market area 1 (North): 132 parcels reduced, 4,349,600 dollars taken off
   - Market area 2 (Old Town): 156 parcels reduced, 5,656,500 dollars taken off
   - Market area 3 (Riverside): 171 parcels reduced, 6,564,800 dollars taken off
   - Market area 4 (East Prairie): 94 parcels reduced, 3,402,200 dollars taken off
   - Market area 5 (Lakes): 166 parcels reduced, 7,095,200 dollars taken off
   - Market area 6 (South): 152 parcels reduced, 6,109,300 dollars taken off
