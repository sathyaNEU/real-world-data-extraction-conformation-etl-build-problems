## Tags

**Domain:** Actuarial Science & Insurance (pricing, ratemaking and credibility).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Corvane Health should put $1,250,000 into its professional liability trust for 2027.**
That is the expected cost, at 2027 cost level, of the Claims first made against the trust in 2027 from incidents on or after each entity's Transition Date, costed on the claims process 2027 will have: the disclosed-harm settlements the Early Resolution Program makes within weeks of the care, the costliest Claims a first claims-made year catches, began at each entity in 2019 and have run in every year since, so each Claim of each entity's experience from its first settlement is costed at its own delay from incident to first making against the days each entity is in the trust. Not $1,000,000, the same construction on the whole 2016 to 2024 experience, because 2016 to 2018 carry the program's requests and the late suits but none of the settlements, so they understate the Claims 2027 will make within weeks. Not the window's expected number of Claims at each class's average Claim cost, because the Claims made within the year are settlements and program requests settled small, while the average carries the demands and suits made a year or more later.

## 2. Critical Components

1. The experience the trust holds is **3,320** Claims, one per incident, from 2016 to 2024 incidents naming Covered Clinicians, on **13,747.1** covered FTE-years.
2. No Claim from a 2016 to 2018 incident was made within **30** days of the care; from each entity's first such Claim in 2019 they run in every year, so the 2027 window is costed on each entity's experience from that month.

## 3. Step-by-Step Solution

1. From rm_claims_register_extract_20261002.csv, kept the incidents dated 2016 to 2024 whose rows name a Covered Clinician (a Schedule B job in clinician_fte_by_month_2016-01_2025-12.csv in the incident month, contracted rows aside), merged each incident's claim numbers into one Claim made on its earliest claim_made_date per the trust agreement's Claim definition, and classed it by its first-named Covered Clinician per Schedule B: 3,320 Claims.
2. Valued each Claim at the paid and reserved indemnity and defense on its Covered Clinicians' rows, trended at 5.0% a year from the incident year to 2027 per the funding policy, and took its delay in days from the incident date to the Claim's first making.
3. Summed the covered paid FTE in clinician_fte_by_month_2016-01_2025-12.csv for 2016 to 2024 under both Schedule B code sets by entity, specialty class and month, each month one twelfth of an FTE-year: 13,747.1 FTE-years.
4. Counted the Claims made within 30 days of their incident by entity and incident year: none from any incident before 2019, and from each entity's first one, between January and July 2019, some in every year to 2024 at a steady rate; took each entity's Claims and payroll months from the month of its first such Claim to December 2024.
5. Took each entity's monthly covered FTE by class in clinician_staffing_plan_2027.xlsx from its Transition Date in Schedule A, each month one twelfth of an FTE-year held through the month's days.
6. Counted each Claim of that experience, at its own trended cost, once for each 2027 FTE-year of its class with at least its own delay left before 31 December 2027, per FTE-year of the class's experience over the same months, and added the classes: $1,250,000 to the nearest $250,000, against $1,000,000 on the whole 2016 to 2024 experience.
7. Matched each entity's open register claims, one per incident, from incidents since its expiring carrier's first term in insurance_premium_history_2016-2026.xlsx, to that carrier's loss run valued 30 September 2026 by insured reference, reading RMN references through rm_carrier_notices_2012_2026.csv and suits under their prior_claim_no: Tolliver Falls 1, Alderwick 3 and the medical group 4 missing.
8. Added the hours on each covered position's lines in hcm_clinician_pay_lines_2026-01_2026-09.csv (covered through hcm_job_profile_crosswalk.csv and Schedule B, a resident's or fellow's additional position left out per the trust agreement's Covered Clinician definition) over 173.33, by the entity of its cost centre in cost_centre_directory_2026.csv: September 2026 188.0, 465.4, 1,040.6 and 108.2.
9. Recommended the 2027 contribution of $1,250,000.

## 4. Deliverable Answers

### trust_funding_2027.xlsx

1. The 2027 contribution: $1,250,000.
2. Open claims under each entity's policies with the carrier it is leaving missing from that carrier's latest loss run, and our reserves on them:
   - Tolliver Falls Hospital (Quillan Mutual): 1 claim, $1,465,000
   - Alderwick Medical Center (Quillan Mutual): 3 claims, $7,000
   - Corvane Medical Group (Stoneleigh Casualty): 4 claims, $54,000
   - Brennick Community Hospital (Stoneleigh Casualty): none
3. Covered clinician FTE the payroll paid in July, August and September 2026:
   - Tolliver Falls Hospital: 188.6, 187.1, 188.0
   - Alderwick Medical Center: 464.5, 463.6, 465.4
   - Corvane Medical Group: 1,037.1, 1,036.8, 1,040.6
   - Brennick Community Hospital: 105.5, 106.7, 108.2

### trustees_paper_2027.pptx

1. Slide 1 states the contribution, $1,250,000, with each entity's Transition Date and months in the trust in 2027.
2. Slide 2 charts each entity's paid covered clinician FTE in July, August and September 2026 as grouped columns, one per month, each labelled with its value.
