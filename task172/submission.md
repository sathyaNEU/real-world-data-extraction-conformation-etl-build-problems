## Tags

**Domain:** Biomedical & Clinical Research (survival and time-to-event analysis).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Continue TALON-2 to its final analysis at 330 events as planned: the conditional power is 100 per cent to the nearest 10 per cent, in Schedule 2's band C (80 per cent or more).** The deciding figure is the final stratified log-rank test projected over the follow-up still to come at each arm's own progression rate before and after the week-12 to week-18 assessments. Not the stratified hazard ratio of 0.91 carried forward, which gives about 5 per cent and a futility stop, because it averages the early period that holds most interim events with the later period that holds most of the events still to come.

## 2. Critical Components

1. The interim cut is 17 November 2026, the date of the 165th BICR-confirmed event; all 450 patients were randomised by then and 267 are still at risk.
2. The stratified hazard ratio is **0.91** (95 per cent CI 0.67 to 1.24), and as a single ratio carried forward it gives a conditional power of about **5** per cent.
3. Ravolimab patients progress at about **1.3** times the placebo rate through the week-12 assessment and about **0.4** times from the week-18 assessment on, and 200 of the 267 patients still at risk are past the week-12 assessment.
4. Projected patient by patient on those rates to the 330th event, the final test rejects in more than 99 per cent of continuations: conditional power **100** per cent to the nearest 10 per cent.

## 3. Step-by-Step Solution

1. Converted each randomisation time in talon2_irt_randomisation_export.csv from UTC to the site's time zone in talon2_sites.json and took the local date as the randomisation date.
2. Built BICR progression-free survival from talon2_bicr_timepoint_reads.csv and the Deaths sheet of talon2_edc_subject_status.xlsx under the SAP's censoring table, found the cut as the date of the 165th event, and dropped every read and death after it.
3. Ran the log-rank test and the Cox model (Efron ties) stratified by the IRT strata, then compared each arm's event rate per patient-month at each assessment visit.
4. Fitted each arm's progression rate before and after the gap between the week-12 and week-18 assessments, followed every patient still at risk forward from the last adequate assessment (withdrawal at the observed rate) to the 330th event in 20,000 simulated continuations, and counted those where the final stratified log-rank test rejects at one-sided 2.5 per cent.
5. For the serious adverse events, took each case's latest report in talon2_pv_sae_line_listing.xlsx, dropped nullified cases and events outside randomisation to the cut, and linked each case to its patient through the screening number, resolving the earlier screen-failure numbers of re-screened patients in talon2_screening_log.csv by site, sex, year of birth and initials.
6. For the liver tests, dated every central sample by its collection date in talon2_edc_central_lab_kit_log.csv (the Melbourne laboratory's transfer carries the date it received the sample), added the local results with their own upper limits, and counted patients above 5 or 3 times the upper limit after the day of the first dose.
7. For exposure, counted the ravolimab or placebo doses the IRT records as administered by the cut, with the EDC exposure pages, and the patients with any dose.
8. Compared the conditional power with Schedule 2's bands and recommended continuing as planned.

## 4. Deliverable Answers

### talon2_interim_recommendation.pdf

1. Recommendation: continue to the final analysis at 330 events as planned (band C).
2. Conditional power, nearest 10 per cent: 100.

### talon2_interim_tables.csv

3. Placebo + GemCis:
   - Patients with a serious adverse event: 113
   - Serious adverse events, all: 170
   - Infections and infestations: 53
   - Hepatobiliary disorders: 57
   - Gastrointestinal disorders: 18
   - Blood and lymphatic system disorders: 23
   - Patients with ALT above 5 x ULN: 2
   - Patients with AST above 5 x ULN: 1
   - Patients with total bilirubin above 3 x ULN: 10
   - Patients who received study treatment: 223
   - Ravolimab or placebo doses given: 1455
4. Ravolimab + GemCis:
   - Patients with a serious adverse event: 132
   - Serious adverse events, all: 222
   - Infections and infestations: 65
   - Hepatobiliary disorders: 74
   - Gastrointestinal disorders: 23
   - Blood and lymphatic system disorders: 30
   - Patients with ALT above 5 x ULN: 10
   - Patients with AST above 5 x ULN: 10
   - Patients with total bilirubin above 3 x ULN: 16
   - Patients who received study treatment: 226
   - Ravolimab or placebo doses given: 1501
