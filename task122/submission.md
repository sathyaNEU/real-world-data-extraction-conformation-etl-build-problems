# task122 submission

## Tags

**Domain:** Biomedical & Clinical Research (longitudinal outcomes with repeated measures: reading a 52-week phase 2b dose-ranging trial's eGFR record for each dose's effect against placebo over a 36-month phase 3).
**Analytical objective:** Experiment & Causal Analysis (which VMK-4410 dose goes into the phase 3, judged by each dose's eGFR difference from placebo after 36 months' treatment).

## 1. Final Recommendation

**Take VMK-4410 20 mg into the phase 3: after 36 months' treatment eGFR would be 3 mL/min/1.73 m2 higher on it than on placebo.**

Not 40 mg (2), which has the largest early fall and only looks best when the one-off recovery after background diuretics were eased is read as a slope; not 10 mg (1), which leads on the week-52 difference alone; not 5 mg (0).

## 2. Critical Components

1. The chronic phase of the eGFR response starts at **week 24**: on 20 and 40 mg the difference from placebo rises from week 12 to week 24, as patients whose loop diuretic was eased from the week-12 visit recover part of the early fall, and is a straight line from week 24 to week 52
2. At month 36, 20 mg leads the runner-up, 40 mg, by **1** mL/min/1.73 m2

## 3. Step-by-Step Solution

1. Took every randomised patient by randomised arm from dm.csv and each patient's first and last dose from ex.csv; a patient whose last dose came before the week-52 visit in sv.csv, or who left the study, stopped study drug for good.
2. From lb.csv took the central laboratory's CKD-EPI 2021 eGFR at the scheduled visits (the first sample of a visit, as section 2 of VMK-4410-202_SAP_v2.0.pdf sets out), baseline the mean of the screening and day-1 values, and set aside values from samples taken after the last dose of a patient who stopped for good, as the estimand in VMK-4410-301_synopsis_draft_v0.3.pdf files it.
3. Took each arm's mean change from baseline at each visit less placebo's.
4. In cm.csv, loop diuretic doses were reduced or stopped at the week-12, 16 and 20 visits in most loop-diuretic patients on 40 mg, many on 20 mg and almost none on placebo, as section 6 of VMK-4410-202_protocol_v3.0.pdf allows from week 12; the 40 mg difference rises 1.8 mL/min/1.73 m2 from week 12 to week 24 and is linear after it.
5. Fitted a straight line through each dose's differences at weeks 24, 32, 40 and 52 and read it at week 156: 20 mg 3, 40 mg 2, 10 mg 1, 5 mg 0 mL/min/1.73 m2.
6. For the tables: serum potassium from every laboratory in lb.csv after the first dose to the last; hyperkalaemia events in ae.csv by group identifier on the SAP's two preferred terms, onset imputed by the SAP's rule; stopping and days on drug from ex.csv, each dosed day counted once, before the sv.csv week-52 visit.
7. Recommendation: VMK-4410 20 mg, 3 mL/min/1.73 m2 above placebo at month 36.

## 4. Deliverable Answers

### VMK-4410_phase3_dose_recommendation.pdf

1. The call: take VMK-4410 20 mg into the phase 3.
2. eGFR difference from placebo after 36 months' treatment, nearest whole mL/min/1.73 m2:
   - 5 mg: 0
   - 10 mg: 1
   - 20 mg: 3
   - 40 mg: 2
3. Chart of each dose's eGFR difference from placebo by month to month 36: the phase 2b visits to week 52 and each dose's chronic-phase line from week 24 carried to month 36, the month-36 values labelled.

### VMK-4410_phase2b_tables.xlsx

1. Patients with a serum potassium above 5.5 mmol/L on treatment:
   - Placebo: 2
   - 5 mg: 4
   - 10 mg: 10
   - 20 mg: 29
   - 40 mg: 68
2. Hyperkalaemia adverse events that began on treatment:
   - Placebo: 1
   - 5 mg: 2
   - 10 mg: 8
   - 20 mg: 28
   - 40 mg: 80
3. Patients who stopped study drug for good before their week-52 visit:
   - Placebo: 5
   - 5 mg: 6
   - 10 mg: 7
   - 20 mg: 9
   - 40 mg: 10
4. The arm's total years on study drug before the week-52 visit, one decimal:
   - Placebo: 147.1
   - 5 mg: 148.4
   - 10 mg: 145.7
   - 20 mg: 146.1
   - 40 mg: 144.7
