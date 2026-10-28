# task236 submission

## Tags

**Domain:** Epidemiology & Public Health (disease surveillance and outbreak anomaly detection: a state health department's weekly influenza report, each health region's notified series read against the sentinel general practice network across a change in the region's testing).
**Analytical objective:** Data Quality Monitoring & Alerting (which regions' notified influenza series carry a testing-change break flag in the week 36 report of 2027).

## 1. Final Recommendation

**Flag the notified influenza series of Far North, Metropolitan South, Metropolitan West and South Coast from the report weeks of their testing changes in the week 36 report, and not those of North Coast, Tablelands, Central West and Metropolitan North.**

Against the sentinel network's influenza activity, the share of influenza infections notified rose 1.87 times in the Far North, 1.53 times in Metropolitan West and 1.53 times in the South Coast as point-of-care testing reached their general practices, and fell to 0.45 of its level in Metropolitan South when its drive-through clinics closed; in the other four regions it moved between 0.99 and 1.01. Not positivity, which flags North Coast, Tablelands, Central West and Metropolitan North, whose positivity rose with the season and with who their changes brought to testing, and misses Far North, whose point-of-care tests find influenza about as often as the referrals they replace. Not the notified counts alone, which rose 2.3 to 5.6 times in every region but Metropolitan South as the season built. Not notifications per influenza-like-illness consultation or per sentinel swab positivity, which flag all eight: RSV filled the consultations before the change weeks, and positivity alone ignores how many people were ill.

## 2. Critical Components

1. Notified cases in the four report weeks before each change and the four from it: Far North **434** and **2,226**; North Coast **763** and **2,267**; Tablelands **286** and **895**; Central West **583** and **1,368**; Metropolitan North **2,459** and **6,943**; Metropolitan South **2,603** and **2,638**; Metropolitan West **1,210** and **6,763**; South Coast **655** and **2,487**
2. Share of influenza infections notified, the four weeks from the change over the four before, against the sentinel network's influenza activity: Far North **1.87**; North Coast **1.01**; Tablelands **1.00**; Central West **1.00**; Metropolitan North **0.99**; Metropolitan South **0.45**; Metropolitan West **1.53**; South Coast **1.53**

## 3. Step-by-Step Solution

1. Took every result in gateway_influenza_results_2027-04-05_to_2027-09-12.csv reporting influenza A or B, preliminary or final, and built cases under CDB-FLU-03 section 2 (influenza_report_data_quality_protocol_CDB-FLU-03.pdf): a person's positives collected within 14 days of the case's first positive specimen are one case, in the report week of that specimen, notified at the first such result's receipt, keys that share a specimen being one person and a key carrying an infant's and an adult's results two (an age one higher is a birthday); 46,380 cases.
2. Placed each case by the residential postcode recorded on any of its results (a preliminary sent without the address taking its final report's), under the concordance in force at the report (postcode_health_region_concordance.csv, rows with no effective_to), a case with none recorded on any result (blank or 0000) by the requesting service's postcode, and left out residents of other states: 44,872 cases in the eight regions with a change in testing_change_register_2027.xlsx.
3. Counted each region's notified cases in the four report weeks before its change week and the four from it (section 4), all notified well before the week 36 cut-off: from 286 (Tablelands, before) to 6,943 (Metropolitan North, after).
4. Measured each region's influenza activity by week from the sentinel network (sentinel_gp_network_protocol_SGP-2027.pdf): influenza-like-illness consultations per 100,000 patients on the lists of the practices that returned in sentinel_gp_weekly_returns_2027_wk14-36.csv, times the share of the tested protocol swabs in sentinel_gp_protocol_swabs_2027_wk14-36.csv with influenza A or B detected.
5. Divided notified cases by influenza activity, each summed over the four weeks, and took the weeks from the change over the weeks before: Far North 1.87, Metropolitan South 0.45, Metropolitan West 1.53 and South Coast 1.53, beyond a quarter either way; North Coast, Tablelands, Central West and Metropolitan North, between 0.99 and 1.01.
6. Counted the season to date, cases with a first positive specimen in weeks 14 to 36 notified by 09:00 on Monday 13 September 2027 (23:00 UTC on Sunday 12 September; section 2): from 1,505 (Tablelands) to 12,037 (Metropolitan North).
7. Divided each region's week 36 cases notified by the cut-off by the estimated resident population at 30 June 2026 of its postcodes under the concordance in force (postcode_erp_30_june_2026.csv; section 3), per 100,000: from 24.9 (Metropolitan South) to 104.0 (South Coast).
8. Flagged Far North, Metropolitan South, Metropolitan West and South Coast from their change weeks and none of the other four, and charted each region's weekly notified cases with its change week and its influenza activity.

## 4. Deliverable Answers

### influenza_testing_break_flags_week36_2027.xlsx

1. One row per region in the file's order, season-to-date notified cases (weeks 14 to 36) whole, week 36 notified rate per 100,000 residents to one decimal:
   - Far North (FN), change in report week 30: flagged, 3,560 notified cases season to date, 53.7 per 100,000 in week 36
   - North Coast (NC), change in report week 30: not flagged, 4,113 notified cases season to date, 39.1 per 100,000 in week 36
   - Tablelands (TB), change in report week 31: not flagged, 1,505 notified cases season to date, 54.6 per 100,000 in week 36
   - Central West (CW), change in report week 31: not flagged, 2,491 notified cases season to date, 50.6 per 100,000 in week 36
   - Metropolitan North (MN), change in report week 30: not flagged, 12,037 notified cases season to date, 36.7 per 100,000 in week 36
   - Metropolitan South (MS), change in report week 31: flagged, 6,133 notified cases season to date, 24.9 per 100,000 in week 36
   - Metropolitan West (MW), change in report week 30: flagged, 11,230 notified cases season to date, 68.4 per 100,000 in week 36
   - South Coast (SC), change in report week 32: flagged, 3,646 notified cases season to date, 104.0 per 100,000 in week 36

### testing_change_breaks_week36_2027.png

2. Eight panels, one per region, of weekly notified cases from week 26 to week 36 with the change week marked by a dashed line; Far North, Metropolitan South, Metropolitan West and South Coast titled as flagged with the weeks the flag covers in red, the other four in grey; the sentinel network's influenza activity drawn as a line on each panel's right axis.
