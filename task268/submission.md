## Tags

**Domain:** Biomedical & Clinical Research, survival and time-to-event analysis (which of Heronmere Health's five hospitals hosts the 2027 heart failure early-diagnosis programme, by the two-year survival from diagnosis of each hospital's patients newly diagnosed with heart failure in 2022 and 2023, from a registry whose follow-up ends when a patient moves beyond its death linkage).
**Analytical objective:** Descriptive & Distribution Analysis (each hospital's distribution of time from heart failure diagnosis to death, read at two years, with the patients lost to a move carried from their recorded clinical state).

## 1. Final Recommendation

**Host the 2027 heart failure early-diagnosis programme at Gullhaven Hospital.**
Its patients newly diagnosed with heart failure in 2022 and 2023 had a two-year survival of 65%, the lowest of the five hospitals and 2 points below Fennick General Hospital's 67%, the next lowest. Not Fennick General Hospital, which Kaplan-Meier with every move as ordinary censoring puts lowest (67% against Gullhaven's 70%), because 526 of Gullhaven's 2,430 patients moved beyond the registry's death linkage within two years, 503 of them in NYHA class III or IV at the visit where they reported the move, and Kaplan-Meier credits them with the survival of the patients who stayed. Not Wrenhaven Medical Center, which comes out lowest only when the 942 patients who left at its 2024 re-consent are dropped or counted as dead.

## 2. Critical Components

1. Gullhaven Hospital's two-year survival from diagnosis, each patient who moved beyond the death linkage carried by the NYHA class recorded at the visit where the move was reported: **65%**.
2. Fennick General Hospital, the next lowest: **67%**; Gullhaven is **2 points** below it.
3. Kaplan-Meier with the moves as ordinary censoring: Fennick **67%**, Gullhaven **70%**.

## 3. Step-by-Step Solution

1. Took every enrolment in hf_registry_patients.csv with a diagnosis date in 2022 or 2023 (charter 3.1 and 3.2, manual 2.1), at the hospital of diagnosis (BRN is Brenmoor Regional, manual 2.2): 8,783 patients.
2. Deaths from fl_death_linkage_2022_2025.xlsx by current record number, legacy numbers through mrn_crosswalk_2024.csv (manual 4.1), and from tristate_exchange_deaths_2022_2025.txt by registry identifier (manual 4.2); a death on or before the second anniversary of diagnosis is a death within two years.
3. Follow-up ends at a relocation (REL) to a state outside Georgia, Alabama and South Carolina (manual 3.3 and 4.3) and at Wrenhaven's re-consent withdrawals (CNR, manual 4.4); relocations to those three states stay in follow-up.
4. Read each clinic visit's NYHA class as one scale (manual 3.2) and measured, hospital by hospital, the chance that a visit in each class ends in a move beyond the linkage: Gullhaven 2.2% at a class III visit and 24.3% at class IV.
5. Weighted each patient still followed, from each visit on, by the inverse of the product of the hospital's chances of staying in reach at the classes recorded so far, and took the weighted product-limit estimate at two years.
6. Two-year survival: Gullhaven 65%, Fennick 67%, Brenmoor 68%, Wrenhaven 72%, Linmoor 73%; carrying the movers instead through the class changes and class-specific death rates of the patients still followed gives the same five figures.
7. Counted the NT-proBNP results each laboratory released in 2025, a corrected result released again under a new accession (same patient and collection time) once, at its final value; a result reported above the analyser's range is at or above 400 pg/mL.
8. Counted the 2025 diagnoses by diagnosis date, a record showing its diagnosis after its enrolment taken at the enrolment date (the diagnosis comes first, manual 2.1), leaving out a 2025 enrolment whose record number maps through the crosswalk to a patient enrolled earlier; inpatient diagnoses are those whose setting reads Inpatient or INPT.

## 4. Deliverable Answers

### hf_programme_site_2027.xlsx

1. Each hospital's two-year survival from diagnosis, patients newly diagnosed with heart failure in 2022 and 2023 (whole percent):
   - Gullhaven Hospital: 65%
   - Fennick General Hospital: 67%
   - Brenmoor Regional Medical Center: 68%
   - Wrenhaven Medical Center: 72%
   - Linmoor Hospital: 73%
2. NT-proBNP tests each hospital's laboratory reported in 2025; of them, at or above 400 pg/mL:
   - Fennick General Hospital: 10,639; 6,991
   - Linmoor Hospital: 8,364; 5,460
   - Brenmoor Regional Medical Center: 8,704; 5,718
   - Gullhaven Hospital: 11,770; 7,723
   - Wrenhaven Medical Center: 9,368; 6,040
3. Patients newly diagnosed with heart failure at each hospital in 2025; of them, diagnosed during an inpatient stay:
   - Fennick General Hospital: 795; 465
   - Linmoor Hospital: 736; 417
   - Brenmoor Regional Medical Center: 734; 404
   - Gullhaven Hospital: 1,222; 723
   - Wrenhaven Medical Center: 833; 494

### service_line_committee_hf_2027.pptx

1. Recommendation: host the programme at Gullhaven Hospital, two-year survival 65%, 2 points below Fennick General Hospital's 67%.
2. Chart of the five hospitals' two-year survival from diagnosis, lowest first, Gullhaven Hospital highlighted.
