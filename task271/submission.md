## Tags

**Domain:** Healthcare Delivery & Health Economics (provider quality and risk adjustment).  
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Name Netherfold Medical Center, Ferncastle Health and Aldermoor University Hospital as the 2027 Pancreatic Surgery Centres.**
Their ratios of observed to expected deaths within 90 days are 0.6, 0.8 and 0.9, the three lowest of the eight, Aldermoor at 0.867 unrounded. Not Farrowmere Regional Medical Center (0.9, 0.921 unrounded), which reaches the three only when the expected deaths leave out the earlier operation on the pancreas or bile ducts that 17.9 per cent of Aldermoor's patients bring (Aldermoor 0.95 on the operation's own record). Not Elmhaven Memorial Hospital (1.0) or Brackwell Medical Center (1.1), above the line on either model.

## 2. Critical Components

1. Operations: **2,022** pancreatic resections at the eight hospitals in 2023 to 2025, **175** deaths within 90 days.
2. An earlier operation on the pancreas or bile ducts, from the patients' earlier admissions since 2016: **17.9** per cent of Aldermoor's patients and **17.1** per cent of Brackwell's, **2.4** to **5.0** per cent elsewhere; coefficient **1.21** in the pooled model.
3. Expected deaths: Netherfold **14.4**, Ferncastle **12.3**, Aldermoor **43.8**, Farrowmere **22.8**, Elmhaven **11.3**, Brackwell **38.1**, Kestwick **18.0**, Yarrowdale **14.3**.
4. Ratios: Netherfold **0.6**, Ferncastle **0.8**, Aldermoor **0.9**, Farrowmere **0.9**, Elmhaven **1.0**, Brackwell **1.1**, Kestwick **1.4**, Yarrowdale **1.4**.

## 3. Step-by-Step Solution

1. Took every Appendix A resection on an adult at the eight hospitals with an operation date in 2023 to 2025 from ulhdc_hbp_discharges_2023_2025.csv, hospital IDs through ulhdc_hospital_directory.xlsx: 2,022 operations.
2. Linked each patient's death through the person key in ulhdc_death_linkage_2016_2026.csv: 175 deaths within 90 days of the operation date (criteria 3.3).
3. Read each patient's earlier admissions in every discharge file from 2016 through the person key and flagged an earlier operation on the pancreas or bile ducts (the pancreas and bile duct operations in ulhdc_procedure_classes.csv): 17.9 per cent of Aldermoor's patients.
4. Fitted one logistic model of death within 90 days on the eight hospitals' operations together, on age, sex, a malignant diagnosis, the operation, the urgency, the seven conditions present on admission and the earlier operation (1.21), and summed each hospital's predicted risks: Aldermoor 43.8 expected deaths.
5. Divided each hospital's deaths by its expected deaths (criteria 3.4) and compared the ratios unrounded (3.5): Aldermoor 0.867 against Farrowmere 0.921.
6. Counted each hospital's resections discharged January to June 2026 in ulhdc_hbp_2026q1q2_revised.csv, two records of one person at one hospital whose stays overlap counted as one operation: Aldermoor 84.
7. Followed each claim in corrisbrook_facility_claims_pancreas_2023_2025.csv through original_claim_id to the claim first received, took each chain's latest version, left out voided claims and their voids, added a stay's interim claims and averaged per stay: Aldermoor 36,722 dollars.
8. Named the three lowest ratios as the 2027 centres: Netherfold Medical Center, Ferncastle Health and Aldermoor University Hospital.

## 4. Deliverable Answers

### pancreatic_centres_2027.xlsx

1. Ratio of observed to expected deaths within 90 days, 2023 to 2025 resections, one decimal:
   - Netherfold Medical Center: 0.6
   - Ferncastle Health: 0.8
   - Aldermoor University Hospital: 0.9
   - Farrowmere Regional Medical Center: 0.9
   - Elmhaven Memorial Hospital: 1.0
   - Brackwell Medical Center: 1.1
   - Kestwick Memorial Hospital: 1.4
   - Yarrowdale Regional Hospital: 1.4
2. The 2027 centres: Netherfold Medical Center, Ferncastle Health and Aldermoor University Hospital.
3. Pancreatic resections discharged January to June 2026:
   - Aldermoor University Hospital: 84
   - Brackwell Medical Center: 66
   - Farrowmere Regional Medical Center: 47
   - Kestwick Memorial Hospital: 36
   - Netherfold Medical Center: 35
   - Yarrowdale Regional Hospital: 29
   - Ferncastle Health: 16
   - Elmhaven Memorial Hospital: 25
4. Average amount allowed per stay for the cooperative's members' pancreatic resection stays discharged 2023 to 2025, whole dollars:
   - Aldermoor University Hospital: $36,722
   - Brackwell Medical Center: $36,265
   - Farrowmere Regional Medical Center: $31,668
   - Kestwick Memorial Hospital: $30,394
   - Netherfold Medical Center: $31,410
   - Yarrowdale Regional Hospital: $30,007
   - Ferncastle Health: $34,135
   - Elmhaven Memorial Hospital: $25,329

### pancreatic_centres_2027.png

1. Dot chart of the eight ratios from lowest to highest, the three centres in plum and the other five in grey, each dot labelled with its ratio, a dashed line at 1.0.
