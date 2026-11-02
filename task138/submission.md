## Tags

**Domain:** Biomedical & Clinical Research (dose-response and PK-PD modelling: the concentration-QTc relationship of an antimuscarinic from its single and multiple ascending dose studies, predicted at each phase 2b dose's high clinical exposure).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Take 50 mg once daily as the highest phase 2b dose: it is the highest dose whose predicted placebo-corrected QTcI change at its high clinical exposure (647 ng/mL) keeps the upper 90% bound below 10 ms, while 100 mg (1,170 ng/mL) breaches it and would need a dedicated QT study.** Not 100 mg: Fridericia's one-third exponent under-corrects the heart-rate rise VLT-317 causes and makes all three doses pass. Not 25 mg: a single QT-RR line through each subject's whole drug-free day takes the night's longer QT for heart rate (mean exponent 0.53 against 0.43 within clock hour) and over-corrects.

## 2. Critical Components

1. High clinical exposure (Day 10 geometric mean Cmax in study 102 times the itraconazole Cmax ratio 2.61): **301 ng/mL** at 25 mg, **647 ng/mL** at 50 mg and **1,170 ng/mL** at 100 mg.
2. Upper 90% bound of the predicted placebo-corrected QTcI change below 10 ms: **25 mg yes, 50 mg yes (6.9 to 8.2 ms), 100 mg no (12.6 to 14.9 ms)**, under every fit that holds clock time fixed (one-hour, half-hour, two- and three-hour bins, cosinor).
3. Each subject's heart-rate exponent, fitted within clock hour on his drug-free Holter segments, averages **0.43**; one line through the whole day gives 0.53.

## 3. Step-by-Step Solution

1. Mapped holter_5min_segments_VLT317-101-102.txt recordings to subjects by the four-digit subject number in PatientID, moved SegmentStart_UTC to Brussels time and kept each subject's readable segments ending before his first dose (dosing_log_VLT317-101-102.csv).
2. Fitted each subject's log QT on log RR with a separate level for every clock hour; the slope is his exponent b (plan section 3).
3. Corrected every readable replicate in the two core-lab transfers (SCREENING_NO and SCRNO mapped to subjects through randomisation_unblinded_VLT317-101-102.xlsx; RR = 60,000/HR for study 102) as QT/RR^b, averaged each time point, and subtracted the same nominal time on Day -1.
4. Paired each time point with its plasma sample (BLQ as zero, the diluted re-assay for results above range) and fitted the plan's mixed model by REML: treatment, concentration, nominal time and centred baseline QTcI, random intercept and concentration slope per subject.
5. Took each phase 2b dose's Day 10 geometric mean Cmax in study 102 times 2.61 (VLT-317-103 synopsis) and predicted the treatment effect plus slope times that exposure with its two-sided 90% interval.
6. For AUC, added each single-dose subject's late samples from ambulatory_lab_results_2026.csv (VOLUNTEER_NO to SCREENING_NO through screening_log_2026.csv, then to subject) and ran the plan's section 6 NCA.
7. For night heart rate, gave each unlabelled Holter recording to the subject whose labelled recording ended within minutes of its first segment with beats, and averaged segments starting 00:00 to 06:00 local time.
8. Recommended 50 mg: the highest dose whose bound stays below 10 ms.

## 4. Deliverable Answers

### cqtc_dose_review.xlsx

1. Call: 50 mg once daily is the highest phase 2b dose that clears the 10 ms bound.
2. High clinical exposure, ng/mL, three significant figures, and whether the upper 90% bound stays below 10 ms:
   - 25 mg: 301 ng/mL, yes
   - 50 mg: 647 ng/mL, yes
   - 100 mg: 1,170 ng/mL, no
3. Geometric mean AUC0-inf after a single dose, ng.h/mL, two significant figures:
   - 25 mg: 1,300
   - 50 mg: 2,500
   - 100 mg: 5,000
   - 200 mg: 9,300
   - 400 mg: 21,000
4. Change in mean heart rate over the segments starting 00:00 to 06:00 local time, night after the first dose against the night before, less the study's placebo change, bpm, one decimal:
   - VLT-317-101, 25 mg: +0.5
   - VLT-317-101, 50 mg: +0.0
   - VLT-317-101, 100 mg: +0.4
   - VLT-317-101, 200 mg: +1.4
   - VLT-317-101, 400 mg: +3.9
   - VLT-317-102, 25 mg: +0.2
   - VLT-317-102, 50 mg: +0.9
   - VLT-317-102, 100 mg: +1.0

### cqtc_dose_memo.pdf

1. Call: 50 mg once daily; 100 mg breaches the 10 ms bound at its high clinical exposure.
2. Chart: placebo-adjusted change in QTcI against plasma concentration, with concentration-decile means, the model line and its 90% band, the 10 ms line and a marker at each dose's high clinical exposure (301, 647 and 1,170 ng/mL).
