## Tags

**Domain:** Actuarial Science & Insurance (claims frequency and severity).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Put the 2027 telematics pilot in Mersey and Pennine.**
Their private cars had the two highest claim frequencies in accident year 2025, 8.9 and 8.2 claims per 100 car-years, and Severn, third at 8.0, is 0.2 below Pennine. Not Mersey and Severn, which the whole book's development gives pooled, by head of claim or by the notified-by field: each blends the claims-management companies that notify Pennine's 2025 injury claims late with faster notifiers, and each misses 2022 in Wessex by 6.8 to 8.5 per cent, outside the Reserving Standard's two.

## 2. Critical Components

1. Claim frequency, accident year 2025, per 100 car-years earned in 2025: Mersey **8.9**; Pennine **8.2**; Severn **8.0**; Wessex **7.3**; Fenland **5.9**; gap from Pennine to Severn **0.2**.
2. Car-years earned in 2025, private cars: Mersey **61,924.81**; Pennine **40,568.81**; Severn **47,215.47**; Wessex **38,108.96**; Fenland **23,927.05**.
3. Claims from 2025 accidents notified by 30 September 2026: Mersey **5,297**; Pennine **2,991**; Severn **3,713**; Wessex **2,681**; Fenland **1,374**.
4. The development by notifying route reproduces accident year 2022 within **1.1** per cent in every region, as the Standard's 3.3 requires.

## 3. Step-by-Step Solution

1. Summed the private-car rows of the 2025 sheet of earned_exposure_2019_2025.xlsx, the earned exposure telematics_pilot_terms_2027.pdf term 3 names: 211,745.10 car-years in all.
2. Counted private-car claims in motor_claims_notified_2019_2026.csv by the Standard's 2.1, each in its region from postcode_district_sales_regions.csv and notified on its UK date: 16,056 claims from 2025 accidents by 30 September 2026.
3. Gave each claim its notifying route, the notified-by field with representatives split by the firm type in claimant_representatives.csv, and measured the whole book's factors from 21 months to final on the closed years 2019 to 2022 (Standard 3.1, 3.2): 3.7 for claims-management companies against 1.2 for solicitors.
4. Re-ran each development on accident year 2022 from 30 September 2023 with 2019 to 2021 (Standard 3.3): the route development is within 1.1 per cent in every region, while pooled, by head of claim and by notified-by field miss Wessex by 6.8 to 8.5 per cent.
5. For cars on cover, applied the address and cover changes in policy_changes_2025_2026.csv effective from each term's start to 30 September 2026 to the private cars on cover that day in policy_vehicles_in_force_20260930.csv, whose rows carry the district and cover at the term's start: Mersey 44,743 COMP, 11,434 TPFT and 4,925 TPO; Pennine 30,213 COMP, 7,051 TPFT and 2,831 TPO; Wessex 30,001 COMP, 5,746 TPFT and 2,037 TPO; Fenland 19,421 COMP, 3,243 TPFT and 1,003 TPO; Severn 36,590 COMP, 7,448 TPFT and 2,919 TPO.
6. Applied the route factors to each region's 2025 notified claims and divided by its car-years: Mersey 8.9; Pennine 8.2; Severn 8.0; Wessex 7.3; Fenland 5.9; Mersey and Pennine host the pilot.

## 4. Deliverable Answers

### telematics_pilot_regions_2027.xlsx

1. Pilot regions: Mersey and Pennine.
2. Claim frequency, accident year 2025, per 100 car-years, one decimal:
   - Mersey: 8.9
   - Pennine: 8.2
   - Severn: 8.0
   - Wessex: 7.3
   - Fenland: 5.9
3. Gap between the second region and the third, Pennine to Severn: 0.2
4. Private cars on cover on 30 September 2026, by cover, whole cars:
   - Mersey: 44,743 COMP, 11,434 TPFT, 4,925 TPO
   - Pennine: 30,213 COMP, 7,051 TPFT, 2,831 TPO
   - Wessex: 30,001 COMP, 5,746 TPFT, 2,037 TPO
   - Fenland: 19,421 COMP, 3,243 TPFT, 1,003 TPO
   - Severn: 36,590 COMP, 7,448 TPFT, 2,919 TPO

### telematics_pilot_regions_2027.pptx

1. Slide 1 names Mersey and Pennine as the pilot regions, at 8.9 and 8.2 claims per 100 car-years.
2. Slide 2 charts the five regions' 2025 frequency as stacked columns, claims notified by 30 September 2026 and claims still to come, the two pilot regions named and the gap of 0.2 stated.
3. Slide 3 sets each development's 2022 back-test beside the Pennine and Severn frequency it gives.
4. Slide 4 carries the cars on cover by region and cover as in the workbook.
