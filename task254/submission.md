# task254: end of pulmonary monitoring for Lyrevo in the RMP update filed with PSUR 6

## Tags

**Domain:** Pharmacology, Pharmacoepidemiology & Safety (time to onset of identified risks from a post-marketing case series, setting the routine monitoring windows of the risk management plan).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**File month 20 of treatment as the end of pulmonary monitoring: by the end of month 20, 95 per cent of interstitial lung disease reactions have begun.**

A reaction can be in the case series only once it has begun, so each one is bounded by its own course's time on treatment at the 30 September 2026 lock, and the reverse-time product-limit estimate on that bound reaches 95 per cent in month 20 and 80 per cent in month 9. Not an earlier month read straight off the reported times to onset: uptake is recent (44,010 of the 74,160 patient-years fall in the twelve months to the lock), so most patients have not been treated long enough for a late reaction to begin, and the series is short of exactly the long onsets that set the 95 per cent cut. Not a Weibull or other fitted curve, which annex 7 section 5 rules out.

## 2. Critical Components

1. 95 per cent of ILD reactions have begun by the end of month **20** of treatment
2. 80 per cent of ILD reactions have begun by the end of month **9** of treatment

## 3. Step-by-Step Solution

1. In `lyrevo_line_listing_PSUR6_DLP20260930.csv` kept each case's latest version received on or before 30 Sep 2026, left out study (ST) reports and cases first received after the lock, and merged duplicates into the master case of `duplicate_register_PSUR6.xlsx` (annex 7 sections 1 and 2).
2. Mapped reactions to the six identified risks with the v4 sheet of `rmp_term_list_version_4.xlsx`, one reaction per case and risk, the earliest onset (annex 7 section 2).
3. Built courses from `lyrevo_dosage_lines_PSUR6.csv`, a new course only after more than 28 days without a dose, and counted time to onset from the first dose of the course in which the reaction began, complete dates only (annex 7 section 3).
4. Dated hepatotoxicity and neutropenia reactions reported without an onset at the first sample in `psp_lab_feed_2023-2026.csv` meeting the case definition, each laboratory's unit and upper limit for the patient's sex taken from `psp_laboratory_register.xlsx` (annex 7 section 4).
5. Bounded each reaction by its course's time on treatment at the lock (days from the course's first dose to 30 Sep 2026) and estimated each risk's onset distribution with the reverse-time product-limit estimator for right-truncated data: ILD reaches 80 per cent in month 9 and 95 per cent in month 20.
6. Counted each risk's cases from launch and among cases first received 1 Oct 2025 to 30 Sep 2026 (annex 7 section 6).
7. Converted supply up to 30 Sep 2026 to patient-years per `PSUR6_section5_exposure_method.docx`: the wholesaler sell-in in `sellin_wholesaler_monthly_2023-2026.csv` net of credit notes with free packs counted, plus the hospital call-offs in `tender_calloffs_FR_IT_ES_2025-2026.xlsx` at 10 packs a shipper case, each national code taken to its pack size through `product_master_national_codes.csv` and `xevmpd_presentations_RVB-417.xml`, one tablet one patient-day: 74,160 patient-years from launch and 44,010 in the twelve months.
8. Recommendation: pulmonary monitoring for patients starting from January 2027 ends after month 20 of treatment.

## 4. Deliverable Answers

### rmp_monitoring_windows_2027.xlsx

1. Interstitial lung disease, 95 per cent of reactions begun: month 20 of treatment.
2. Months of treatment by which 80 and 95 per cent of reactions have begun:
   - Interstitial lung disease: 80 per cent by month 9, 95 per cent by month 20
   - Herpes zoster: 80 per cent by month 11, 95 per cent by month 21
   - Serious infections: 80 per cent by month 7, 95 per cent by month 18
   - Venous thromboembolism: 80 per cent by month 6, 95 per cent by month 16
   - Hepatotoxicity: 80 per cent by month 4, 95 per cent by month 9
   - Neutropenia: 80 per cent by month 3, 95 per cent by month 8
3. Reporting rates per 1,000 patient-years, from launch (3 Apr 2023 to 30 Sep 2026) and for the twelve months to the lock (1 Oct 2025 to 30 Sep 2026):
   - Interstitial lung disease: 8.1 from launch, 8.3 for the twelve months
   - Herpes zoster: 23.7 from launch, 24.2 for the twelve months
   - Serious infections: 27.2 from launch, 27.2 for the twelve months
   - Venous thromboembolism: 11.2 from launch, 11.2 for the twelve months
   - Hepatotoxicity: 20.5 from launch, 20.5 for the twelve months
   - Neutropenia: 18.8 from launch, 18.5 for the twelve months
4. Patient-years, nearest 10:
   - From launch to 30 Sep 2026: 74,160
   - Of which on 15 mg tablets: 46,320
   - Of which on 30 mg tablets: 27,840
   - 1 Oct 2025 to 30 Sep 2026: 44,010

### onset_windows_by_risk.svg

1. Cumulative share of reactions begun by month of treatment, months 0 to 24, one panel per identified risk, each risk's 95 per cent window marked at its month: interstitial lung disease 20, herpes zoster 21, serious infections 18, venous thromboembolism 16, hepatotoxicity 9, neutropenia 8.
2. Title giving the ILD month: "Pulmonary monitoring to month 20: by then 95% of interstitial lung disease reactions have begun".
