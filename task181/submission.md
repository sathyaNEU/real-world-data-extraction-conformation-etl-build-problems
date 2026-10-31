## Tags

> **Domain:** Epidemiology and public health, disease surveillance and outbreak anomaly detection.
> **Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**Send the hotspot response for morbidity weeks 41 to 44 to San Roque, Bagumbayan and Maligaya, and to no other barangay.**
San Roque is where the window's cases were infected far past the plan's trigger of 40, at the Dalisay Industrial Estate, though its own residents number only 14 of the cases. Not Tabing-Ilog, Pulong Bayabas, Malinta, Kanluran, Burol or Silangan, which are over 40 by home address only because their working residents were infected at the estate. Bagumbayan and Maligaya stay in: their outbreaks are at home, across every age.

## 2. Critical Components

1. The plan counts the window's cases where they were infected (section 4.3), and no shipped file records a place of infection, so it is estimated.
2. By home address, Bagumbayan, Maligaya, Tabing-Ilog, Pulong Bayabas, Malinta, Kanluran, Burol and Silangan are over 40 and San Roque is under it.
3. In the six barangays beside the estate the rise is among working-age residents only, and CBMS Table 4 puts a large share of their workers in San Roque.
4. Placing each barangay's working-age cases where its workers work puts San Roque, Bagumbayan and Maligaya at 40 or more and every other barangay under it, at any share of the working day from a half to all of it and by the inversion of Table 4.

## 3. Step-by-Step Solution

1. From dengue_line_list_2022_2027.csv, kept each case number's latest row, dropped Not a case and residents of other towns, merged patients notified twice (same initials, sex, age, barangay and onset), mapped spellings and Santo Tomas Puroks 5 to 8 to Santo Tomas Norte, and dated each case by onset or, where blank, consultation (plan 4.1, 4.2): by home address eight barangays have 40 or more cases with onset in weeks 37 to 40.
2. Measured each barangay's working-age cases (15 to 64) in the window against its own 2022 to 2026 ratio of working-age to other cases: the six barangays beside the estate carry nearly all the excess.
3. Fitted each barangay's rate as a workplace to the barangays' excess against their employed residents' place-of-work counts in cbms_2025_dalisay_city.xlsx Table 4 (non-negative least squares) and placed the excess there, and split every working-age case by the Table 3 employment rate and Table 4 shares at 0.5 to 1.0 of the day at work: San Roque, Bagumbayan and Maligaya reach 40 under every placement, no other barangay does.
4. Hospitals: in dmc_dengue_inpatient_census_2027.csv, stitched each hospital number's ward segments into stays (a segment starting the minute the last ended with no disposition continues it) and counted stays by first ward entry; in ddh_dengue_admissions_2027.xlsx, counted every weekly sheet's rows by date admitted (month first) less the patients moved from Dalisay Medical Center, matched by age, sex and address within eight hours of the transfer (plan 4.4).
5. Larval survey: keyed each house by barangay, purok and house number, a house positive where any row found larvae or pupae, and took positive houses over houses inspected (plan 4.6).
6. Laboratory: removed the runs cho_lab_run_log_2027.json rejects, took each person (initials, birth date and sex) at the collection week of the first positive result, by test (plan 4.5).
7. Recommendation: send the hotspot response to San Roque, Bagumbayan and Maligaya.

## 4. Deliverable Answers

### dengue_hotspots_mw41_44_2027.pdf

1. Barangays going under the response: San Roque, Bagumbayan, Maligaya.
2. Every other barangay marked out, Tabing-Ilog, Pulong Bayabas, Malinta, Kanluran, Burol and Silangan among them.
3. Bar chart on page 2: the window's cases infected in each barangay, the trigger of 40 drawn across it, San Roque, Bagumbayan and Maligaya in red.

### response_figures_2027.csv

1. Dalisay Medical Center dengue admissions, whole numbers:
   - Week 33: 54
   - Week 34: 65
   - Week 35: 68
   - Week 36: 79
   - Week 37: 80
   - Week 38: 68
   - Week 39: 53
   - Week 40: 60
2. Dalisay Doctors' Hospital dengue admissions, whole numbers:
   - Week 33: 33
   - Week 34: 31
   - Week 35: 58
   - Week 36: 39
   - Week 37: 42
   - Week 38: 27
   - Week 39: 40
   - Week 40: 32
3. House index, September 2027 round, per cent to one decimal:
   - Bayanihan: 15.4
   - Dila: 24.1
   - Liwayway: 13.1
   - Lumbia: 18.8
   - Mabini: 12.7
   - Mangga: 25.8
   - Parian: 17.0
   - Rizal: 4.5
   - San Isidro: 4.9
   - Santa Cruz: 15.1
   - Tagumpay: 20.9
   - Talon: 20.7
4. Patients whose first positive dengue test was an NS1, whole numbers:
   - Week 35: 52
   - Week 36: 60
   - Week 37: 52
   - Week 38: 57
   - Week 39: 68
   - Week 40: 31
5. Patients whose first positive dengue test was an IgM, whole numbers:
   - Week 35: 7
   - Week 36: 10
   - Week 37: 9
   - Week 38: 10
   - Week 39: 10
   - Week 40: 5
