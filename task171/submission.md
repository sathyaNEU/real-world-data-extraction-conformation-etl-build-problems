## Tags

**Domain:** Pharmacology, Pharmacoepidemiology & Safety, population pharmacokinetics and exposure-response (a phase 3 induction dose for an anti-IL-23 antibody in ulcerative colitis, forecast from the exposure-response of the one dose a phase 2b trial tested, under the sponsor's dose-selection charter).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Corvane should carry dovikizumab 300 mg IV at weeks 0, 4 and 8 into phase 3.**
The forecast week-12 clinical remission rate is 40.7 per cent at 300 mg, 40.9 at 600 mg and 41.0 at 900 mg, so 300 mg is 0.3 points under the highest forecast, inside the charter's 5 points, and the lowest candidate there. The forecast rests on the week-4 pre-dose concentration, which the dose sets before healing begins: remitters and non-remitters had the same week-4 concentrations, and only later, as the colitis healed and clearance fell, did remitters' concentrations pull ahead, so an exposure-response on the later concentrations is steep because of the remission it is meant to predict and files 900 mg.

## 2. Critical Components

1. Remitters' to non-remitters' geometric mean concentration among the dovikizumab patients with a valid sample at the visit (pre-dose samples drawn after the infusion started set aside at every visit, SAP 6.8): **1.02** before the week-4 infusion, **2.26** before the week-8 infusion and **3.12** at week 12.
2. On the week-4 pre-dose concentration, week-12 remission is flat across exposure (quartiles 43, 37, 39 and 45 per cent), so every candidate dose forecasts about the same remission: **300 mg within 0.43 points of the highest forecast** under every model on that concentration, with or without the randomisation stratum and baseline weight and modified Mayo score.
3. The exposure-response analysis set is the **455** of 480 dovikizumab patients with a valid week-4 pre-dose concentration; in that arm **15** week-4 and 20 week-8 pre-dose samples drawn after the infusion had started (laboratory UTC against the site's local start) are not pre-dose samples (SAP 6.8).

## 3. Step-by-Step Solution

1. Joined cvn2184_201_randomisation_log.csv (randomisation to site-subject numbers and arms), cvn2184_201_serum_concentrations.csv (reportable results, ng/mL results divided by 1,000, below-limit results as below 0.100 ug/mL), cvn2184_201_infusion_records.csv and cvn2184_201_site_list.csv (the site's country for its summer time) to the week-12 remission flag in cvn2184_201_efficacy_database_lock.csv.
2. Set aside each pre-dose sample whose UTC collection time was at or after the infusion's local start converted to UTC (SAP 6.8).
3. Compared remitters' and non-remitters' concentrations at weeks 4, 8 and 12 (geometric means): equal at week 4, apart after, as clearance falls with healing.
4. Fitted week-12 remission (logistic) on the log week-4 pre-dose concentration with the randomisation stratum, scaled each patient's concentration by dose over 600 (investigator's brochure 5.2) and averaged the predicted remission over the exposure-response analysis set (charter 4).
5. Applied the charter's rule (charter 5): the lowest dose whose forecast is no more than 5 points below the highest, compared unrounded.
6. For safety, rebuilt each adverse event from cvn2184_201_adverse_events.csv by chaining a patient's records of one preferred term from review to review while ongoing, taking the onset entered at the latest review (an onset first entered as the visit or admission date is corrected there) and serious if any record is; then SAP 6.2 to 6.6 against the infusion dates and each patient's last visit in cvn2184_201_visit_dates.csv.
7. For immunogenicity, rebuilt each draw as the patient's samples on one collection date in cvn2184_201_ada_results.csv (the backup aliquot's tube arrives on a manifest reading Unscheduled), took each tier's latest result in a run brightwater_ada_run_log.csv accepts, and applied SAP 6.7 against the baseline draw.
8. For the e-diary, gave each entry to the registration holding the handset on its diary date (cvn2184_201_ediary_handset_log.csv), traced a registration the randomisation log does not know to the patient who handed that handset over the same day (the four closed sites' patients), took the last entry for each date and applied SAP 6.10 at days 43, 57 and 71.

## 4. Deliverable Answers

### induction_dose_memo.docx

1. Phase 3 induction dose: 300 mg IV at weeks 0, 4 and 8.
2. Forecast week-12 clinical remission: 300 mg 40.7 per cent, 600 mg 40.9 per cent, 900 mg 41.0 per cent (300 mg 0.3 points below the highest).

### phase2b_induction_tables.xlsx

1. Patients with at least one treatment-emergent serious infection: dovikizumab 12, placebo 7.
2. Patients with at least one infusion-related reaction: dovikizumab 32, placebo 13.
3. Serious infections per 100 patient-years: dovikizumab 11.0, placebo 14.7.
4. Treatment-emergent ADA incidence, per cent: dovikizumab week 4 2.5, week 8 5.6, week 12 8.7; placebo week 4 0.4, week 8 1.3, week 12 2.2.
5. Patients in symptomatic remission on the e-diary: dovikizumab week 6 133, week 8 196, week 10 208; placebo week 6 17, week 8 32, week 10 35.

### exposure_response_chart.png

1. Week-12 remission by quartile of the week-4 pre-dose concentration, flat, with the three dose forecasts; beside it the remitter to non-remitter concentration ratio rising from 1.02 at week 4 to 3.12 at week 12.
