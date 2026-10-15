## Tags

**Domain:** Biomedical & Clinical Research, medical imaging reader study evaluation (which AI reading-support tool a breast screening service licenses, from three fully crossed reader studies of its film readers' probability-of-malignancy ratings).
**Analytical objective:** Descriptive & Distribution Analysis (how reader accuracy and each tool's gain in it are distributed over readers and examinations, and whether the gain holds for the service's readers and examinations).

## 1. Final Recommendation

**License Halvic Breast for two years from 1 April 2027.**
Its gain of 0.026 in the readers' average area under the ROC curve is the only one whose two-sided 95 per cent interval lies wholly above zero once the panel's readers and the study's examinations are both treated as samples of the service's (protocol, section 4). Not Ondrix Mammo (gain 0.042), whose gain swings from reader to reader (3 of its 10 readers read worse with it), so its interval crosses zero once readers are random. Not Lumidra Detect (gain 0.047), whose gain varies from examination to examination the same way for every reader, so its interval crosses zero once examinations are random.

## 2. Critical Components

1. Gain in the readers' average area under the empirical ROC curve, with the tool minus unaided: Lumidra Detect **0.047**, Ondrix Mammo **0.042**, Halvic Breast **0.026**
2. Two-sided 95 per cent interval with readers and examinations both random: wholly above zero for **Halvic Breast only**; Ondrix Mammo's and Lumidra Detect's cross zero

## 3. Step-by-Step Solution

1. Read readpoint_MBS-AI-01_export_2026-04-24.csv, readpoint_MBS-AI-02_export_2026-07-08.csv and readpoint_MBS-AI-03_export_2026-09-25.csv (the last in the platform's newer layout, the probability as a fraction), kept each reader's last submission for each case and condition (readpoint_export_fields_v4.pdf) and joined each study's sheet of reader_study_case_sets_2026.xlsx, which leaves out the practice cases: 10 readers, 300 examinations (75 malignant) and two conditions per study.
2. Computed each reader's area under the empirical ROC curve of the probability-of-malignancy ratings against the Outcome column (Mann-Whitney, ties counted half) and each tool's gain as the panel's average area with the tool minus its average unaided (ai_evaluation_protocol_v2.pdf, section 3): 0.047 for Lumidra Detect, 0.042 for Ondrix Mammo and 0.026 for Halvic Breast.
3. Built each tool's interval for the service's film readers reading its screening examinations (protocol, section 4) with readers and examinations both random, by Obuchowski-Rockette analysis with jackknife covariances and Hillis's degrees of freedom (the same as DBM): only Halvic Breast's lies wholly above zero; Ondrix Mammo's gain varies across its readers (3 of 10 read worse with it) and Lumidra Detect's across its examinations, and both intervals cross zero.
4. Counted the completed MAMS and MAMT studies dated 1 October 2025 to 30 September 2026 in ris_mammography_studies_2025-10_2026-09.csv, dropped each legacy (LR) record that repeats a new-system (MW) record for the same woman, location, code and day at the same clock time or exactly an hour later, and counted mobile units to the site hosting them on the day in mobile_unit_visits_2025-26.xlsx: 45,878 screening studies.
5. Counted the screening episodes as quote_lumidra_detect_2027.pdf defines them, one per woman and screening round with its technical repeats, each counted with its routine study: 44,262 screening episodes.
6. Counted the staff in film_reader_workforce_2026-10.xlsx who read films and are in post on 1 April 2027, once per professional registration: 27 film readers.
7. Priced each first contract year from quote_ondrix_mammo_2027.pdf (per screening study received, with its minimum annual charge), quote_lumidra_detect_2027.pdf (per screening episode and per film reader account) and quote_halvic_breast_2027.pdf (per film reader seat and per screening site), one-off fees included and VAT excluded.
8. License Halvic Breast.

## 4. Deliverable Answers

### ai_reading_support_decision_2027.pdf

1. The recommendation: license Halvic Breast for two years from 1 April 2027, the only tool whose gain has a 95 per cent interval wholly above zero for the service's film readers and screening examinations.
2. Why not Ondrix Mammo: its gain varies from reader to reader (3 of its 10 readers read worse with it), so its interval crosses zero once the readers are treated as a sample of the service's.
3. Why not Lumidra Detect: its gain varies from examination to examination the same way for every reader, so its interval crosses zero once the examinations are treated as a sample of the service's.

### ai_tool_evaluation_2027.xlsx

1. Each tool's gain in its readers' average area under the ROC curve and whether it meets the protocol:
   - Lumidra Detect: 0.047, does not meet the protocol
   - Ondrix Mammo: 0.042, does not meet the protocol
   - Halvic Breast: 0.026, meets the protocol
2. Screening studies sent for reading from 1 October 2025 to 30 September 2026, each site with its mobile units:
   - Corrowby Road Breast Unit: 11,569
   - Wendlow Breast Screening Centre: 7,298
   - Copse Lane Breast Screening Centre: 13,253
   - Tallowmere Park Breast Unit: 13,758
3. Film readers in post on 1 April 2027: 27
4. Each tool's cost in its first contract year under its vendor's quote, excluding VAT:
   - Lumidra Detect: £110,745
   - Ondrix Mammo: £89,122
   - Halvic Breast: £101,750

### reader_study_gains.png

1. Each tool's gain with its two-sided 95 per cent interval, readers and examinations both random, against a zero line: Halvic Breast's interval wholly above zero, Ondrix Mammo's and Lumidra Detect's crossing it.
