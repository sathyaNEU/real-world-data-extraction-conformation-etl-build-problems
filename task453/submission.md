# task453 submission

## Tags

**Domain:** Survey Research & Official Statistics, seasonal adjustment and official time-series production (a published unemployment rate carried across a questionnaire redesign phased in through the Labour Force Survey's rotation groups, and the statutory trigger that reads it restated).
**Analytical objective:** Data Extraction & Conformation (ETL) (the survey's two collection systems, CAI 2014 for the previous questionnaire and ICS for the redesigned one, conformed with the region concordance and the release into one series on the redesigned basis).

## 1. Final Recommendation

**Restate the Regional Employment Support Act's trigger at 6.5 per cent, which designates Eastern Ranges, Western Coast, River Delta and Highlands for 2027.**

With every rotation group answering it, the redesigned questionnaire puts the published national unemployment rate 0.5 percentage points higher than the previous questionnaire would have for the same months, read interview by interview against the same interview on the previous questionnaire. Not the gap between the two questionnaires' rotation groups in July to November 2025 (1.2 points, a trigger of 7.2 per cent): it sets the redesign's first interviews against the previous questionnaire's last ones, and first interviews ran 1.3 points above the six-interview average. Not one effect with the interview number held fixed (a trigger of 6.3 or 6.4 per cent): the redesign lowers the rate at a first interview and raises it from the second, where dependent interviewing applies, and one effect leans on the first interviews the phase-in is made of. North Coast misses the restated trigger by 0.06 points.

## 2. Critical Components

1. The change in the published national rate is **+0.5** percentage points (0.4848 before rounding), the average of the six interview effects.
2. Before July 2025 a first interview ran **1.3** points above the average of the six interviews.
3. The restated trigger is **6.5** per cent (6.0 plus 0.5, Act section 9(2)).
4. The 2026 twelve-month averages of the designated regions: Eastern Ranges **6.58**, Western Coast **6.64**, River Delta **7.44**, Highlands **8.32**; North Coast **6.44**.

## 3. Step-by-Step Solution

1. Conformed lfs_cai2014_estimation_cells_2022-01_2025-11.csv (weighted thousands by LFSTAT, regions on the 2019 codes to December 2024, through region_classification_concordance_2019_2025.csv) and lfs_ics_estimation_cells_2025-07_2026-12.csv (weighted persons) into weighted unemployed and labour force by month, region and rotation group; each month reproduces Table 2 of lfs_release_2026-12_tables.xlsx.
2. Gave each rotation group its interview number from the replacement schedule in lfs_redesigned_questionnaire_methodology_note.pdf section 1: before July 2025 a first interview ran 1.3 points above the six-interview average, and the gap between the two questionnaires' groups in July to November 2025 is 1.2 points, mostly that bias.
3. Read the redesign's effect at each interview number against the same interview number on the previous questionnaire, month and region held fixed, January 2022 to December 2026: negative at the first interview, positive at the second to sixth.
4. Averaged the six effects as a published estimate averages the six rotation groups (methodology note section 1): +0.4848, +0.5 points rounded (Act section 9(2)).
5. Restated the trigger: 6.0 plus 0.5 is 6.5 per cent (sections 8 and 9).
6. Averaged each region's twelve 2026 rates in Table 2 (section 3) and designated those at or above 6.5 (section 7): Eastern Ranges 6.58, Western Coast 6.64, River Delta 7.44 and Highlands 8.32; North Coast at 6.44 falls 0.06 short.
7. Counted responding dwellings in lfs_fieldwork_contacts_2026q4.parquet: a dwelling is its dwelling_ref with the month it entered (contact month less interview_no plus one), responding on outcome 11 or 12, placed in its region by lfs_psu_region_lookup_2025.csv: 88,040 in all.
8. Recommendation: restate the trigger at 6.5 per cent, designating Eastern Ranges, Western Coast, River Delta and Highlands.

## 4. Deliverable Answers

### trigger_restatement_determination_2027.pdf

1. Restated trigger: 6.5 per cent.
2. The change in the published unemployment rate it rests on: +0.5 percentage points.
3. Regions designated for 2027: Eastern Ranges, Western Coast, River Delta and Highlands; not designated: Capital, Harbour, North Coast, Inland Plains and Southern Valleys.
4. Responding dwellings, October to December 2026, each dwelling counted once:
   - Capital: 14,827
   - Harbour: 11,749
   - North Coast: 9,532
   - Inland Plains: 10,842
   - Eastern Ranges: 7,981
   - Southern Valleys: 9,007
   - Western Coast: 7,532
   - River Delta: 10,008
   - Highlands: 6,562
   - All regions: 88,040
5. Line chart on page 1: the national unemployment rate as published (the original series) and on the redesigned basis, January 2024 to December 2026, July to November 2025 shaded as both questionnaires in the field, the 6.0 and 6.5 per cent triggers drawn at their values, titled with the 0.5-point change.

### regional_unemployment_redesigned_basis_2024-2026.csv

6. One row per region and month, January 2024 to December 2026 (324 rows), with the published rate and the rate on the redesigned basis to one decimal place: to June 2025 the published rate plus 0.5, from July 2025 as published (July to November 2025 marked as both questionnaires in the field).
