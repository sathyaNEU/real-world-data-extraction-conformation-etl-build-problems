## Tags

**Domain:** Actuarial Science & Insurance (pricing, ratemaking and credibility).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Corvane Health should put $1,250,000 into its professional liability trust for 2027.**
That is the expected cost, at 2027 cost level, of the Claims first made against the trust in 2027 from incidents on or after each entity's Transition Date, each Claim of the 2016 to 2024 experience costed at its own delay from incident to first making against the days each entity is in the trust. Not the window's expected number of Claims at each class's average Claim cost, because the Claims made within the year are disclosed harm settled within weeks and program requests settled small, while the average carries the demands and suits made a year or more later. Not the same count at the average cost of the Claims made within a year, or along a severity curve fitted on the delay, because the window counts the costly Claims made within weeks far more often than the cheap ones made months later, and the cost falls and then rises with the delay.

## 2. Critical Components

1. The experience is **3,043** Claims, one per incident, from 2016 to 2024 incidents naming Covered Clinicians.
2. It rests on **13,747.1** covered FTE-years in the 2016 to 2024 payroll.

## 3. Step-by-Step Solution

1. From rm_claims_register_extract_20261002.csv, kept the incidents dated 2016 to 2024 whose rows name a Covered Clinician (a Schedule B job in clinician_fte_by_month_2016-01_2025-12.csv in the incident month, contracted rows aside), merged each incident's claim numbers into one Claim made on its earliest claim_made_date per the trust agreement's Claim definition, and classed it by its first-named Covered Clinician per Schedule B: 3,043 Claims.
2. Valued each Claim at the paid and reserved indemnity and defense on its Covered Clinicians' rows, trended at 5.0% a year from the incident year to 2027 per the funding policy, and took its delay in days from the incident date to the Claim's first making.
3. Summed the covered paid FTE in clinician_fte_by_month_2016-01_2025-12.csv for 2016 to 2024 under both Schedule B code sets by specialty class, each month one twelfth of an FTE-year: 13,747.1 FTE-years.
4. Took each entity's monthly covered FTE by class in clinician_staffing_plan_2027.xlsx from its Transition Date in Schedule A, each month one twelfth of an FTE-year held through the month's days.
5. Counted each experience Claim, at its own trended cost, once for each 2027 FTE-year of its class with at least its own delay left before 31 December 2027, per FTE-year of the class's experience, and added the classes: $1,250,000 to the nearest $250,000.
6. Matched each entity's open register claims, one per incident, from incidents since its expiring carrier's first term in insurance_premium_history_2016-2026.xlsx, to that carrier's loss run valued 30 September 2026 by insured reference, reading RMN references through rm_carrier_notices_2012_2026.csv, suits under their prior_claim_no, and a suit the run carries with no insured reference by entity, date of loss and claim type: Alderwick 4 and the medical group 5 missing.
7. Added the hours on each covered position's lines in hcm_clinician_pay_lines_2026-01_2026-09.csv (covered through hcm_job_profile_crosswalk.csv and Schedule B; a worker paid on a resident or fellow position for the month is a trainee that month, a TRM termination payout not counting, and his additional position is left out per the trust agreement's Covered Clinician definition) over 173.33, by the entity of its cost centre in cost_centre_directory_2026.csv: September 2026 188.0, 465.4, 1,040.6 and 108.2.
8. Recommended the 2027 contribution of $1,250,000.

## 4. Deliverable Answers

### trust_funding_2027.xlsx

1. The 2027 contribution: $1,250,000.
2. Open claims under each entity's policies with the carrier it is leaving missing from that carrier's latest loss run, and our reserves on them:
   - Tolliver Falls Hospital (Quillan Mutual): none
   - Alderwick Medical Center (Quillan Mutual): 4 claims, $839,000
   - Corvane Medical Group (Stoneleigh Casualty): 5 claims, $16,000
   - Brennick Community Hospital (Stoneleigh Casualty): none
3. Covered clinician FTE the payroll paid in July, August and September 2026:
   - Tolliver Falls Hospital: 188.6, 187.1, 188.0
   - Alderwick Medical Center: 464.5, 463.6, 465.4
   - Corvane Medical Group: 1,037.1, 1,036.8, 1,040.6
   - Brennick Community Hospital: 105.5, 106.7, 108.2

### trustees_paper_2027.pptx

1. Slide 1 states the contribution, $1,250,000, with each entity's Transition Date and months in the trust in 2027.
2. Slide 2 charts each entity's paid covered clinician FTE in July, August and September 2026 as grouped columns, one per month, each labelled with its value.
