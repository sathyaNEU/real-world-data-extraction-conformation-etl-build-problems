## Tags

**Domain:** Biomedical & Clinical Research (dose-response and PK/PD modelling: a phase 3 dose for a monoclonal antibody in plaque psoriasis).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Take HB-231 200 mg into phase 3: it is the lowest candidate dose whose expected week-16 PASI 75 response in the phase 3 population is at least 70 per cent.**
Not 100 mg, whose VELA-2 arm reached 81.0 per cent: the VELA-3 candidates weigh more (110.9 kg against 84.7 kg), HB-231's troughs fall with body weight and response follows the trough, so 100 mg falls under the bar in the phase 3 population. Not 50 mg, under the bar in both.

## 2. Critical Components

1. Expected week-16 PASI 75 response in the phase 3 population against the 70 per cent bar: 50 mg **below it**, 100 mg **below it**, 200 mg **at or above it**.
2. HB-231's week-16 trough concentration falls with body weight: clearance rises about in proportion to weight (exponent **1.2** in the population PK model of the VELA-2 troughs).
3. Mean body weight: VELA-2 patients **84.7 kg**, VELA-3 feasibility candidates **110.9 kg** (US weights converted from pounds).

## 3. Step-by-Step Solution

1. Study day 1 is each patient's first dose in the dosing log; PASI baseline is the last assessment on or before it (the Finnish sites' "Day 1" record, not their "Baseline" screening record).
2. Week-16 PASI 75 and PASI 90 under the SAP's composite: rescue (ATC D07AC or D07AD, or phototherapy) started after the first dose and on or before the week-16 assessment, or no week-16 PASI, is non-response.
3. Troughs: the Lund laboratory's ng/mL divided by 1,000, below-limit samples dropped; log concentration per mg regressed on visit and log(weight/85).
4. Each active-arm patient's typical week-16 trough from dose and weight; logistic regression of the composite PASI 75 on its log.
5. Each feasibility candidate's typical trough at 50, 100 and 200 mg (pounds times 0.45359237); the fitted response averaged over the candidates gives the expected response per dose.
6. The lowest dose at or above 70 per cent is 200 mg.
7. Itch: entries placed on the local diary day (after midnight and before 03:00 to the evening before); weekly means over study days -7 to -1, 78 to 84 and 106 to 112 with at least four entries; responders at least 4 points down from a baseline of at least 4 with no rescue by the week's last day.

## 4. Deliverable Answers

### hb231_phase3_dose_recommendation.docx

1. Phase 3 dose: HB-231 200 mg every four weeks.
2. Expected week-16 PASI 75 in the phase 3 population against the 70 per cent bar: 50 mg below, 100 mg below, 200 mg at or above.
3. Chart of each candidate dose's expected response against the bar.

### hb231_phase2b_tables.csv

1. PASI 75 at week 16 (per cent): Placebo 6.0, HB-231 25 mg 25.0, HB-231 50 mg 43.0, HB-231 100 mg 81.0, HB-231 200 mg 89.0.
2. PASI 90 at week 16 (per cent): Placebo 0.0, HB-231 25 mg 11.0, HB-231 50 mg 22.0, HB-231 100 mg 66.0, HB-231 200 mg 74.0.
3. Itch NRS responders at week 12 (per cent of patients with a baseline weekly score of at least 4): Placebo 12.0, HB-231 25 mg 35.1, HB-231 50 mg 55.8, HB-231 100 mg 86.5, HB-231 200 mg 90.1.
4. Itch NRS responders at week 16 (per cent of patients with a baseline weekly score of at least 4): Placebo 12.0, HB-231 25 mg 30.9, HB-231 50 mg 54.7, HB-231 100 mg 85.4, HB-231 200 mg 86.8.
