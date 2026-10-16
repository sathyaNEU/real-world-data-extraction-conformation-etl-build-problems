## Tags

> **Domain:** General Statistics & Data Science (missing data, censoring and measurement error).
> **Analytical objective:** Data Quality Monitoring & Alerting.

## 1. Final Recommendation

**Suppress the NEET rates of City East, City West and Riverside and the higher-education entry rates of Hill Country and Northern Plains; publish the NEET rates of Southern Shore, Glen Villages and Upper Valley and the higher-education entry rates of Old Docks and Mill Towns with the standard flag; publish the other 14 statistics under caution.**

The 2025 follow-up, in five districts chosen across the island's range, found nonrespondents with 2.46 times the odds of NEET and 0.41 times the odds of higher education that their allocations gave them, in every district and band it covered, so each nonrespondent's allocation moves on the odds scale, shifting the district rates from 0.34 points (Southern Shore's NEET rate) to 3.72 (Riverside's NEET rate). Not a flat 14.5-point NEET gap per nonrespondent, which would suppress the NEET rates of Hill Country and Northern Plains, leave those of City East and City West under caution and miss the higher-education suppressions; not a gap or a ratio per attainment band, which the follow-up's districts reject.

## 2. Critical Components

1. Comparable follow-up cases (resolved, still nonrespondents in the 2025 final file, one per case): **3,134**
2. The follow-up's departure on the odds scale, one ratio across its districts and bands: NEET **2.46**, higher education **0.41**
3. Nonrespondents on the 2026 frame: **7,641** of **47,734** leavers

## 3. Step-by-Step Solution

1. Mapped each school on leaver_destinations_frame_2026.csv to its 2026 district in school_register.xlsx: 47,734 leavers, 7,641 of them nonrespondents carrying allocations.
2. Joined nonresponse_followup_2025_outcomes.csv to leaver_destinations_final_2025.csv through followup_case_crosswalk_2025.csv, one outcome per case, keeping resolved cases whose leaver has no form in the final file (QS-4 section 6): 3,134 of the 3,617 cases drawn.
3. Regressed each case's found destination (field report section 5) on the logit of its 2025 allocation: slope 0.99 for NEET and 1.03 for higher education, a constant shift on the odds scale, while the points gap (14.5 for NEET pooled) grows with the allocation.
4. Fitted the departure with each case's allocation on the logit scale as offset: odds ratio 2.46 for NEET and 0.41 for higher education.
5. Moved each 2026 nonrespondent's NEET and higher-education allocation by those odds ratios and summed to the district (QS-4 section 3): shifts from 0.34 (Southern Shore NEET rate) to 3.72 (Riverside NEET rate) points.
6. Banded each unrounded shift under QS-4 section 4: 5 suppressed, 5 standard, 14 caution.
7. Headline rates (QS-4 section 2): returned forms read with activity_codes.csv, online returns on build 7 (the 2025 edition) with the order the 2025 final file's processed destinations show, plus allocations, over every leaver.
8. Banded leavers on state_exam_points_2026.csv's final points (methodology section 5) for the band table.

## 4. Deliverable Answers

### leaver_destinations_2026_quality_flags.xlsx

1. Each statistic's headline rate (per cent, one decimal) and flag, in district code order:
   - City East (ED01): NEET rate 28.2, suppressed; higher-education entry rate 27.0, caution
   - City West (ED02): NEET rate 23.3, suppressed; higher-education entry rate 32.7, caution
   - Riverside (ED03): NEET rate 16.8, suppressed; higher-education entry rate 39.2, caution
   - Old Docks (ED04): NEET rate 30.9, caution; higher-education entry rate 16.8, standard
   - Coastal Strip (ED05): NEET rate 12.8, caution; higher-education entry rate 45.9, caution
   - Southern Shore (ED06): NEET rate 1.5, standard; higher-education entry rate 74.2, caution
   - Glen Villages (ED07): NEET rate 3.0, standard; higher-education entry rate 62.7, caution
   - Upper Valley (ED08): NEET rate 2.8, standard; higher-education entry rate 74.4, caution
   - Hill Country (ED09): NEET rate 4.5, caution; higher-education entry rate 65.5, suppressed
   - Northern Plains (ED10): NEET rate 7.9, caution; higher-education entry rate 55.2, suppressed
   - Market Towns (ED11): NEET rate 9.4, caution; higher-education entry rate 52.0, caution
   - Mill Towns (ED12): NEET rate 31.6, caution; higher-education entry rate 12.5, standard
2. Attainment bands across the island (leavers; headline NEET and higher-education entry rates, per cent, one decimal):
   - AB1: 11,331 leavers, NEET rate 2.4, higher-education entry rate 80.7
   - AB2: 14,483 leavers, NEET rate 6.9, higher-education entry rate 57.9
   - AB3: 12,699 leavers, NEET rate 17.6, higher-education entry rate 29.6
   - AB4: 9,221 leavers, NEET rate 36.5, higher-education entry rate 10.3
